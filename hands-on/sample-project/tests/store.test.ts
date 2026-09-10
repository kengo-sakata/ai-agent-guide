import { describe, expect, it } from "vitest";
import { createTodo, deleteTodo, findTodo, listTodos, updateTodo } from "@/lib/store";

describe("store", () => {
  it("createTodo は未完了のTODOを追加する", () => {
    const before = listTodos().length;
    const todo = createTodo({ title: "テスト用のTODO" });

    expect(todo.title).toBe("テスト用のTODO");
    expect(todo.completed).toBe(false);
    expect(listTodos()).toHaveLength(before + 1);
  });

  it("updateTodo は完了フラグを切り替えられる", () => {
    const todo = createTodo({ title: "切り替え対象" });

    const updated = updateTodo(todo.id, { completed: true });

    expect(updated?.completed).toBe(true);
    expect(findTodo(todo.id)?.completed).toBe(true);
  });

  it("updateTodo は存在しないIDに対して undefined を返す", () => {
    expect(updateTodo("does-not-exist", { completed: true })).toBeUndefined();
  });

  it("deleteTodo は削除できたかどうかを返す", () => {
    const todo = createTodo({ title: "削除対象" });

    expect(deleteTodo(todo.id)).toBe(true);
    expect(deleteTodo(todo.id)).toBe(false);
    expect(findTodo(todo.id)).toBeUndefined();
  });
});
