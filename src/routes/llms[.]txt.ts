import { createFileRoute } from '@tanstack/react-router'
import { allPosts } from 'content-collections'
import { site, siteUrl } from '@/lib/seo'

export const Route = createFileRoute('/llms.txt')({
  server: {
    handlers: {
      GET: () => {
        const posts = [...allPosts].sort((a, b) => b.createdAt.localeCompare(a.createdAt))
        const content = [
          `# ${site.name}`,
          '',
          `> ${site.description}`,
          '',
          'This is Sandon’s personal website. Posts describe his own projects, experiences and interests.',
          '',
          '## Pages',
          '',
          `- [About Sandon](${siteUrl('/')}): Background, current work and interests.`,
          `- [Posts](${siteUrl('/posts')}): All published writing.`,
          '',
          '## Posts',
          '',
          ...posts.map((post) => `- [${post.title}](${siteUrl(`/posts/${post.slug}`)}): ${post.summary}`),
          '',
          '## Optional',
          '',
          '- [GitHub](https://github.com/sandonl): Public source code.',
          '- [LinkedIn](https://linkedin.com/in/sandonlai): Professional profile.',
          '',
        ].join('\n')
        return new Response(content, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } })
      },
    },
  },
})
