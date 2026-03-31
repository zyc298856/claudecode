import { getAllPosts } from "@/lib/posts";
import { PostCard } from "@/components/post-card";

export default function Home() {
  const posts = getAllPosts().slice(0, 5);

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <section className="mb-12">
        <h1 className="text-3xl font-bold">My Tech Blog</h1>
        <p className="mt-3 text-gray-600">
          记录编程技术、项目实践和学习心得。
        </p>
      </section>
      <section>
        <h2 className="text-xl font-semibold mb-4">最新文章</h2>
        {posts.map((post) => (
          <PostCard key={post.slug} post={post} />
        ))}
      </section>
    </div>
  );
}
