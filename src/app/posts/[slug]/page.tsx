import { allPosts } from "content-collections";
import { notFound } from "next/navigation";
export default async function PostPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const slug = (await params).slug;

  const post = allPosts.find((post) => post.slug === slug);

  if (!post) {
    notFound();
  }

  return (
    <article className="py-6">
      <div className="mb-8">
        <h1 className="mb-2 text-3xl font-bold">{post.title}</h1>
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <time dateTime={post.createdAt}>
            {new Date(post.createdAt).toLocaleDateString("en-US", {
              year: "numeric",
              month: "long",
              day: "numeric",
            })}
          </time>
          <div className="flex gap-2">
            {post.tags.map((tag) => (
              <span
                key={tag}
                className="inline-flex items-center rounded-md bg-secondary px-2 py-1 text-xs"
              >
                {tag}
              </span>
            ))}
          </div>
          <div className="text-xs text-muted-foreground"> - {post.author}</div>
        </div>
      </div>
      <div className="mt-8 prose prose-invert prose-headings:scroll-mt-20 text-sm max-w-none">
        <post.mdxContent />
      </div>
    </article>
  );
}
