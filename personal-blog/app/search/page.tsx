import { getSearchIndex } from "@/lib/search";
import { SearchBar } from "@/components/search-bar";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "搜索 - My Tech Blog",
};

export default function SearchPage() {
  const entries = getSearchIndex();

  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">搜索</h1>
      <SearchBar entries={entries} />
    </div>
  );
}
