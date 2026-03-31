import { notFound } from "next/navigation";
import { MDXRemote } from "next-mdx-remote/rsc";
import { getAllPosts, getPostBySlug } from "@/lib/posts";
import { mdxComponents } from "@/components/mdx-components";
import Link from "next/link";
import type { Metadata } from "next";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateStaticParams() {
  const posts = getAllPosts();
  return posts.map((post) => ({ slug: post.slug }));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const { meta } = getPostBySlug(slug);
  return {
    title: `${meta.title} - My Tech Blog`,
    description: meta.description,
  };
}

export default async function PostPage({ params }: PageProps) {
  const { slug } = await params;
  try {
    const { meta, content } = getPostBySlug(slug);

    return (
      <article className="max-w-3xl mx-auto px-4 py-8">
        <header className="mb-8">
          <h1 className="text-3xl font-bold">{meta.title}</h1>
          <div className="mt-3 flex items-center gap-3 text-sm text-gray-400">
            <time dateTime={meta.date}>{meta.date}</time>
            <Link
              href={`/categories/${encodeURIComponent(meta.category)}`}
              className="px-2 py-0.5 rounded bg-blue-50 text-blue-600"
            >
              {meta.category}
            </Link>
            {meta.tags.map((tag) => (
              <span key={tag} className="text-gray-400">#{tag}</span>
            ))}
          </div>
        </header>
        <div className="prose-custom">
          <MDXRemote source={content} components={mdxComponents} />
        </div>
        <div className="mt-12 pt-6 border-t border-gray-200">
          <Link href="/posts" className="text-blue-600 hover:underline">
            &larr; 返回文章列表
          </Link>
        </div>
      </article>
    );
  } catch {
    notFound();
  }
}
