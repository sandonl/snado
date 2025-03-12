import { Link } from "next-view-transitions";
import { allPosts } from "content-collections";
import { Badge } from "@/components/ui/badge";
import LetterSwapPingPong from "@/components/letter-swap-ping-pong";

export default function BlogOverview() {
  return (
    <div>
      <div className="flex pb-8">
        <LetterSwapPingPong label="Posts" className="text-3xl font-bold" />
      </div>
      <div className="space-y-8">
        {allPosts.map((post) => (
          <article key={post.slug} className="border-b pb-8">
            <div className="flex items-center justify-between">
              <Link
                href={`/posts/${post.slug}`}
                className="text-xl font-semibold hover:text-primary/80"
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
            <p className="mt-2 text-sm text-muted-foreground">{post.summary}</p>
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
