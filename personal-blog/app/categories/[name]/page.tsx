import { getAllCategories, getPostsByCategory } from "@/lib/posts";
import { PostCard } from "@/components/post-card";
import { notFound } from "next/navigation";
import type { Metadata } from "next";

interface PageProps {
  params: Promise<{ name: string }>;
}

export async function generateStaticParams() {
  const categories = getAllCategories();
  return categories.map((name) => ({ name: encodeURIComponent(name) }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { name } = await params;
  return { title: `分类: ${decodeURIComponent(name)} - My Tech Blog` };
}

export default async function CategoryPage({ params }: PageProps) {
  const { name } = await params;
  const category = decodeURIComponent(name);
  const posts = getPostsByCategory(category);

  if (posts.length === 0) notFound();

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">分类: {category}</h1>
      {posts.map((post) => (
        <PostCard key={post.slug} post={post} />
      ))}
    </div>
  );
}
