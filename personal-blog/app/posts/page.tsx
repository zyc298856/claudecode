import { getAllPosts } from "@/lib/posts";
import { PostCard } from "@/components/post-card";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "所有文章 - My Tech Blog",
  description: "浏览所有技术文章",
};

export default function PostsPage() {
  const posts = getAllPosts();

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">所有文章</h1>
      {posts.map((post) => (
        <PostCard key={post.slug} post={post} />
      ))}
    </div>
  );
}
