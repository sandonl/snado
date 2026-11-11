export const site = {
  name: 'Sandon Lai',
  url: 'https://www.sandonl.dev',
  description: 'Sandon Lai is an AI and software engineer in Melbourne, building tools for legal professionals and writing about software, AI and language learning.',
}

export function siteUrl(path: string) {
  return new URL(path, site.url).href
}

// Escape HTML-sensitive characters so content cannot close the JSON-LD script tag.
export function structuredData(data: Record<string, unknown>) {
  return {
    type: 'application/ld+json',
    children: JSON.stringify(data).replace(/</g, '\\u003c'),
  }
}

export function pageHead({ title, description, path, type = 'website' }: {
  title: string
  description: string
  path: string
  type?: 'website' | 'article'
}) {
  const url = siteUrl(path)
  return {
    meta: [
      { title },
      { name: 'description', content: description },
      { property: 'og:title', content: title },
      { property: 'og:description', content: description },
      { property: 'og:url', content: url },
      { property: 'og:type', content: type },
      { property: 'og:site_name', content: site.name },
      { name: 'twitter:card', content: 'summary' },
      { name: 'twitter:title', content: title },
      { name: 'twitter:description', content: description },
    ],
    links: [{ rel: 'canonical', href: url }],
  }
}
