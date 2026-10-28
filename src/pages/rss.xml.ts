// RSS feed - using Astro's built-in RSS functionality
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const crystals = await getCollection('crystals');
  
  return rss({
    title: 'Crystalica — Enciclopedia Cristalelor',
    description: 'Descoperă proprietățile energetice, istorii, chakre, zodiac și folosințe practice pentru fiecare cristal.',
    site: context.site,
    items: crystals.map(crystal => ({
      title: crystal.data.name,
      link: `/cristale/${crystal.data.slug}`,
      description: crystal.data.description,
      pubDate: new Date(),
    })),
  });
}