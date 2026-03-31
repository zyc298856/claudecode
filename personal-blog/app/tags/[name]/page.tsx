import { getAllTags, getPostsByTag } from "@/lib/posts";
import { PostCard } from "@/components/post-card";
import { notFound } from "next/navigation";
import type { Metadata } from "next";

interface PageProps {
  params: Promise<{ name: string }>;
}

export async function generateStaticParams() {
  const tags = getAllTags();
  return tags.map((name) => ({ name: encodeURIComponent(name) }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { name } = await params;
  return { title: `标签: ${decodeURIComponent(name)} - My Tech Blog` };
}

export default async function TagPage({ params }: PageProps) {
  const { name } = await params;
  const tag = decodeURIComponent(name);
  const posts = getPostsByTag(tag);

  if (posts.length === 0) notFound();

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">标签: #{tag}</h1>
      {posts.map((post) => (
        <PostCard key={post.slug} post={post} />
      ))}
    </div>
  );
}
