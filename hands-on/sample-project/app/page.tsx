import TodoApp from "@/components/TodoApp";

export default function Page() {
  return (
    <main>
      <h1>TODO</h1>
      <p className="subtitle">ハンズオン用のサンプルTODO管理アプリ</p>
      <div className="panel">
        <TodoApp />
      </div>
    </main>
  );
}
