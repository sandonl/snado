import { createFileRoute, Link } from '@tanstack/react-router'
import { allPosts } from 'content-collections'
import LetterSwapPingPong from '@/components/letter-swap-ping-pong'

export const Route = createFileRoute('/posts/')({
  component: PostsPage
})

function PostsPage() {
  const posts = [...allPosts].sort(
    (a, b) =>
      new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  )

  return (
    <main className="min-h-[calc(100vh-16rem)] border-b pb-12 pt-8">
      <h1 className="mb-12 flex pb-3">
        <LetterSwapPingPong label="Posts" className="text-3xl font-bold" />
      </h1>
      <div className="border-t border-zinc-800">
        {posts.map((post, index) => (
          <article key={post.slug} className="grid grid-cols-[3rem_1fr] border-b border-zinc-800 py-6 sm:grid-cols-[5rem_1fr]">
            <span className="font-mono text-xs text-zinc-600">
              {String(index + 1).padStart(2, '0')}
            </span>
            <div>
              <h2 className="mb-2 text-sm font-bold text-zinc-100">
                <Link
                to="/posts/$slug"
                params={{ slug: post.slug }}
                className="rounded-sm transition-colors hover:text-zinc-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-zinc-400"
              >
                {post.title}
              </Link>
              </h2>
              <p className="max-w-md text-xs leading-5 text-zinc-400">{post.summary}</p>
              <div className="mt-3 flex flex-wrap items-baseline gap-x-4 gap-y-1 text-xs leading-5 text-zinc-500">
              <time dateTime={post.createdAt}>
                {new Date(post.createdAt).toLocaleDateString("en-US", {
                  year: "numeric",
                  month: "long",
                  day: "numeric",
                })}
              </time>
              <span>{post.tags.join(' · ')}</span>
              </div>
            </div>
          </article>
        ))}
      </div>
    </main>
  )
}
