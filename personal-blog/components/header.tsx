import Link from "next/link";

export function Header() {
  return (
    <header className="border-b border-gray-200">
      <nav className="max-w-3xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="text-xl font-bold">
          My Tech Blog
        </Link>
        <div className="flex gap-6 text-sm">
          <Link href="/posts" className="hover:text-blue-600">文章</Link>
          <Link href="/categories" className="hover:text-blue-600">分类</Link>
          <Link href="/tags" className="hover:text-blue-600">标签</Link>
          <Link href="/search" className="hover:text-blue-600">搜索</Link>
          <Link href="/about" className="hover:text-blue-600">关于</Link>
        </div>
      </nav>
    </header>
  );
}
