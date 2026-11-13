// SPDX-License-Identifier: AGPL-3.0-or-later
//
// @tauri-apps/plugin-sql replacement: SQLite (sql.js / WASM) persisted to IndexedDB.
import initSqlJs, { type Database as SqlDb, type SqlValue } from "sql.js";
import wasmUrl from "sql.js/dist/sql-wasm.wasm?url";

const IDB_NAME = "warid-db";
const IDB_STORE = "files";

function idb(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(IDB_NAME, 1);
    req.onupgradeneeded = () => req.result.createObjectStore(IDB_STORE);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}
async function idbGet(key: string): Promise<Uint8Array | null> {
  const db = await idb();
  return new Promise((resolve, reject) => {
    const r = db.transaction(IDB_STORE).objectStore(IDB_STORE).get(key);
    r.onsuccess = () => resolve((r.result as Uint8Array) ?? null);
    r.onerror = () => reject(r.error);
  });
}
async function idbPut(key: string, val: Uint8Array): Promise<void> {
  const db = await idb();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(IDB_STORE, "readwrite");
    tx.objectStore(IDB_STORE).put(val, key);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

/** tauri-plugin-sql uses sqlx-style `$1` placeholders; SQLite wants `?1`. */
function toSqlite(query: string): string {
  return query.replace(/\$(\d+)/g, "?$1");
}

export default class Database {
  private saveTimer: ReturnType<typeof setTimeout> | null = null;
  private constructor(private readonly db: SqlDb, private readonly key: string) {
    const flush = () => void this.flush();
    document.addEventListener("visibilitychange", () => {
      if (document.visibilityState === "hidden") flush();
    });
    window.addEventListener("pagehide", flush);
  }

  static async load(path: string): Promise<Database> {
    const SQL = await initSqlJs({ locateFile: () => wasmUrl });
    const saved = await idbGet(path);
    return new Database(saved ? new SQL.Database(saved) : new SQL.Database(), path);
  }

  private scheduleSave() {
    if (this.saveTimer) clearTimeout(this.saveTimer);
    this.saveTimer = setTimeout(() => void this.flush(), 400);
  }
  private async flush() {
    if (this.saveTimer) {
      clearTimeout(this.saveTimer);
      this.saveTimer = null;
    }
    await idbPut(this.key, this.db.export());
  }

  async execute(query: string, bindValues?: unknown[]): Promise<{ rowsAffected: number; lastInsertId?: number }> {
    const sql = toSqlite(query);
    if (bindValues && bindValues.length) {
      this.db.run(sql, bindValues as SqlValue[]);
    } else {
      this.db.run(sql);
    }
    const rowsAffected = this.db.getRowsModified();
    this.scheduleSave();
    return { rowsAffected };
  }

  async select<T>(query: string, bindValues?: unknown[]): Promise<T> {
    const stmt = this.db.prepare(toSqlite(query));
    try {
      if (bindValues && bindValues.length) stmt.bind(bindValues as SqlValue[]);
      const rows: Record<string, unknown>[] = [];
      while (stmt.step()) rows.push(stmt.getAsObject());
      return rows as unknown as T;
    } finally {
      stmt.free();
    }
  }

  async close(): Promise<boolean> {
    await this.flush();
    this.db.close();
    return true;
  }
}
