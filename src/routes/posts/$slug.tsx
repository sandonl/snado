import { pageHead, siteUrl, structuredData } from '@/lib/seo'
import { createFileRoute, notFound } from '@tanstack/react-router'
import { allPosts } from 'content-collections'
import { MDXContent } from '@content-collections/mdx/react'
import { Quote } from '@/components/ui/quote'

// Custom components available in MDX files
const mdxComponents = {
  Quote,
}

export const Route = createFileRoute('/posts/$slug')({
  loader: ({ params }) => {
    const post = allPosts.find((p) => p.slug === params.slug)
    if (!post) {
      throw notFound()
    }
    return { post }
  },
  head: ({ loaderData }) => {
    if (!loaderData) {
      return { meta: [{ title: 'Post not found | Sandon Lai' }, { name: 'robots', content: 'noindex' }] }
    }
    const { post } = loaderData
    const head = pageHead({
      title: `${post.title} | Sandon Lai`,
      description: post.summary,
      path: `/posts/${post.slug}`,
      type: 'article',
    })
    return {
      ...head,
      meta: [
        ...head.meta,
        { property: 'article:published_time', content: post.createdAt },
        { name: 'author', content: post.author },
      ],
      scripts: [structuredData({
        '@context': 'https://schema.org',
        '@type': 'BlogPosting',
        headline: post.title,
        description: post.summary,
        datePublished: post.createdAt,
        author: { '@type': 'Person', '@id': siteUrl('/#person'), name: post.author, url: siteUrl('/') },
        mainEntityOfPage: siteUrl(`/posts/${post.slug}`),
        keywords: post.tags,
        inLanguage: 'en',
      })],
    }
  },
  component: PostPage,
  notFoundComponent: () => (
    <div className="py-6">
      <h1 className="text-2xl font-bold">Post not found</h1>
      <p className="mt-2 text-muted-foreground">The requested post does not exist.</p>
    </div>
  )
})

function PostPage() {
  const { post } = Route.useLoaderData()
  
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
        <MDXContent code={post.mdx} components={mdxComponents} />
      </div>
    </article>
  )
}
