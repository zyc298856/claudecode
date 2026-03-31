import { getAllCategories, getAllPosts } from "@/lib/posts";
import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "分类 - My Tech Blog",
};

export default function CategoriesPage() {
  const categories = getAllCategories();
  const posts = getAllPosts();

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">分类</h1>
      <div className="space-y-4">
        {categories.map((category) => {
          const count = posts.filter((p) => p.category === category).length;
          return (
            <Link
              key={category}
              href={`/categories/${encodeURIComponent(category)}`}
              className="flex items-center justify-between p-4 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors"
            >
              <span className="font-medium">{category}</span>
              <span className="text-sm text-gray-400">{count} 篇文章</span>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
