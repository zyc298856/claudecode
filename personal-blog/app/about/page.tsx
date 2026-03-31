import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "关于 - My Tech Blog",
};

export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">关于我</h1>
      <div className="prose-custom space-y-4">
        <p>
          嗨，欢迎来到我的技术博客。
        </p>
        <p>
          我是一名软件开发者，热爱编程和技术探索。在这里，我会分享：
        </p>
        <ul className="list-disc pl-6 space-y-1">
          <li>编程技术和最佳实践</li>
          <li>项目开发中的经验和教训</li>
          <li>新技术的学习和评测</li>
          <li>日常开发中的小技巧</li>
        </ul>
        <p>
          如果你对某篇文章有疑问或建议，欢迎通过评论区留言。
        </p>
      </div>
    </div>
  );
}
