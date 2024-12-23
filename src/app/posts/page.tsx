import { Link } from "next-view-transitions";
import { allPosts } from "content-collections";
import { Badge } from "@/components/ui/badge";

export default function BlogOverview() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Posts</h1>
      <div className="space-y-8">
        {allPosts.map((post) => (
          <article key={post.slug} className="border-b pb-8">
            <div className="flex items-center justify-between">
              <Link
                href={`/posts/${post.slug}`}
                className="text-2xl font-semibold hover:text-primary/80"
              >
                {post.title}
              </Link>
              <p className="text-muted-foreground">
                {new Date(post.createdAt).toLocaleDateString("en-US", {
                  year: "numeric",
                  month: "long",
                  day: "numeric",
                })}
              </p>
            </div>
            <p className="mt-2">{post.summary}</p>
            <div className="mt-4 flex gap-2">
              {post.tags.map((tag) => (
                <Badge key={tag} variant="outline">
                  {tag}
                </Badge>
              ))}
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
