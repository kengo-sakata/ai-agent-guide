import type { Todo } from "@/lib/types";

/**
 * インメモリのデータストア。
 * 開発サーバーのプロセスが再起動するとデータは初期状態に戻る。
 */
const todos: Todo[] = [
  {
    id: "1",
    title: "サンプルプロジェクトを起動する",
    completed: true,
    createdAt: "2026-04-01T09:00:00.000Z",
  },
  {
    id: "2",
    title: "TODOを追加してみる",
    completed: false,
    createdAt: "2026-04-01T09:05:00.000Z",
  },
  {
    id: "3",
    title: "完了フラグを切り替えてみる",
    completed: false,
    createdAt: "2026-04-01T09:10:00.000Z",
  },
];

let nextId = todos.length + 1;

export function listTodos(): Todo[] {
  return [...todos];
}

export function findTodo(id: string): Todo | undefined {
  return todos.find((todo) => todo.id === id);
}

export function createTodo(input: { title: string }): Todo {
  const todo: Todo = {
    id: String(nextId++),
    title: input.title,
    completed: false,
    createdAt: new Date().toISOString(),
  };
  todos.push(todo);
  return todo;
}

export function updateTodo(
  id: string,
  patch: { title?: string; completed?: boolean },
): Todo | undefined {
  const todo = findTodo(id);
  if (!todo) {
    return undefined;
  }
  if (patch.title !== undefined) {
    todo.title = patch.title;
  }
  if (patch.completed !== undefined) {
    todo.completed = patch.completed;
  }
  return todo;
}

export function deleteTodo(id: string): boolean {
  const index = todos.findIndex((todo) => todo.id === id);
  if (index === -1) {
    return false;
  }
  todos.splice(index, 1);
  return true;
}
