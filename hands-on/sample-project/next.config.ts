import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Next.js が AGENTS.md / CLAUDE.md を自動生成する機能を無効化している。
  // ハンズオン（03）で「CLAUDE.md が無い状態」から始めるため。
  agentRules: false,
};

export default nextConfig;
