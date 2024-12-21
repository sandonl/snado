import Link from "next/link";
import { allPosts } from "content-collections";

export default function BlogOverview() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Posts</h1>
      <div className="space-y-8">
        {allPosts.map((post) => (
          <article key={post._meta.path} className="border-b pb-8">
            <Link
              href={`/blog/${post._meta.path}`}
              className="text-2xl font-semibold hover:underline"
            >
              {post.title}
            </Link>
            <p className="text-gray-500 mt-2">
              {/* {new Date(post.).toLocaleDateString("en-US", {
                year: "numeric",
                month: "long",
                day: "numeric",
              })} */}
            </p>
            <p className="mt-2">{post.summary}</p>
            <div className="mt-4">
              {/* {post.tags.map((tag) => (
                <span
                  key={tag}
                  className="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2"
                >
                  #{tag}
                </span>
              ))} */}
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
