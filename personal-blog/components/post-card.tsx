import Link from "next/link";
import type { PostMeta } from "@/lib/posts";

export function PostCard({ post }: { post: PostMeta }) {
  return (
    <article className="py-6 border-b border-gray-100 last:border-0">
      <Link href={`/posts/${post.slug}`}>
        <h2 className="text-xl font-semibold hover:text-blue-600 transition-colors">
          {post.title}
        </h2>
      </Link>
      <p className="mt-2 text-gray-600 text-sm">{post.description}</p>
      <div className="mt-3 flex items-center gap-3 text-xs text-gray-400">
        <time dateTime={post.date}>{post.date}</time>
        <Link
          href={`/categories/${encodeURIComponent(post.category)}`}
          className="px-2 py-0.5 rounded bg-blue-50 text-blue-600 hover:bg-blue-100"
        >
          {post.category}
        </Link>
        {post.tags.map((tag) => (
          <Link
            key={tag}
            href={`/tags/${encodeURIComponent(tag)}`}
            className="px-2 py-0.5 rounded bg-gray-50 text-gray-600 hover:bg-gray-100"
          >
            #{tag}
          </Link>
        ))}
      </div>
    </article>
  );
}
