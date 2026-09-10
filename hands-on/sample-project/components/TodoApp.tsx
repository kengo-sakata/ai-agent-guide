"use client";

import { useCallback, useEffect, useState } from "react";
import type { Todo } from "@/lib/types";

type ApiError = {
  error?: { message?: string };
};

async function readErrorMessage(response: Response, fallback: string) {
  try {
    const body = (await response.json()) as ApiError;
    return body.error?.message ?? fallback;
  } catch {
    return fallback;
  }
}

export default function TodoApp() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [title, setTitle] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const loadTodos = useCallback(async () => {
    const response = await fetch("/api/todos");
    if (!response.ok) {
      setMessage(await readErrorMessage(response, "TODOの取得に失敗しました"));
      return;
    }
    const body = (await response.json()) as { todos: Todo[] };
    setTodos(body.todos);
  }, []);

  useEffect(() => {
    loadTodos().finally(() => setLoading(false));
  }, [loadTodos]);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage(null);

    const response = await fetch("/api/todos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });

    if (!response.ok) {
      setMessage(await readErrorMessage(response, "TODOの追加に失敗しました"));
      return;
    }

    setTitle("");
    await loadTodos();
  }

  async function handleToggle(todo: Todo) {
    setMessage(null);

    const response = await fetch(`/api/todos/${todo.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed: !todo.completed }),
    });

    if (!response.ok) {
      setMessage(await readErrorMessage(response, "TODOの更新に失敗しました"));
      return;
    }

    await loadTodos();
  }

  async function handleDelete(todo: Todo) {
    setMessage(null);

    const response = await fetch(`/api/todos/${todo.id}`, { method: "DELETE" });

    if (!response.ok) {
      setMessage(await readErrorMessage(response, "TODOの削除に失敗しました"));
      return;
    }

    await loadTodos();
  }

  return (
    <>
      {message && <p className="message">{message}</p>}

      <form className="todo-form" onSubmit={handleSubmit}>
        <input
          id="new-todo-title"
          name="title"
          value={title}
          aria-label="新しいTODO"
          placeholder="新しいTODOを入力"
          onChange={(event) => setTitle(event.target.value)}
        />
        <button type="submit" disabled={title.trim() === ""}>
          追加
        </button>
      </form>

      {loading ? (
        <p className="empty">読み込み中...</p>
      ) : todos.length === 0 ? (
        <p className="empty">TODOはありません</p>
      ) : (
        <ul className="todo-list">
          {todos.map((todo) => (
            <li
              key={todo.id}
              className={todo.completed ? "todo-item completed" : "todo-item"}
            >
              <input
                id={`todo-${todo.id}`}
                type="checkbox"
                checked={todo.completed}
                onChange={() => handleToggle(todo)}
              />
              <label htmlFor={`todo-${todo.id}`}>{todo.title}</label>
              <button
                type="button"
                className="delete-button"
                onClick={() => handleDelete(todo)}
              >
                削除
              </button>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
