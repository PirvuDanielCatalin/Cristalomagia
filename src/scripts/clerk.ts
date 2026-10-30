import { Clerk } from '@clerk/clerk-js';

export type CollectionState = 'p' | 'w';
export type CollectionsMap = Record<string, CollectionState>;

interface CrystalicaWindow extends Window {
  __crystalicaClerk?: Clerk;
  __crystalicaClerkReady?: Promise<void>;
}

const env = import.meta.env as Record<string, string | undefined>;
const publishableKey = env.PUBLIC_CLERK_PUBLISHABLE_KEY;
const browserWindow = typeof window !== 'undefined' ? (window as CrystalicaWindow) : null;

let instance: Clerk | null = null;
let ready: Promise<void> = Promise.resolve();

if (browserWindow) {
  if (!publishableKey) {
    console.warn('[Crystalica] PUBLIC_CLERK_PUBLISHABLE_KEY lipsește — autentificarea este dezactivată.');
  } else {
    try {
      if (!browserWindow.__crystalicaClerk) {
        const clerkInstance = new Clerk(publishableKey);
        browserWindow.__crystalicaClerk = clerkInstance;
        browserWindow.__crystalicaClerkReady = clerkInstance
          .load({
            appearance: {
              variables: {
                colorPrimary: '#3d9b91',
                fontFamily: "'DM Sans', system-ui, -apple-system, sans-serif",
                borderRadius: '0.5rem',
              },
            },
          })
          .catch((error) => {
            console.error('[Crystalica] Clerk nu a putut fi inițializat.', error);
          });
      }

      instance = browserWindow.__crystalicaClerk ?? null;
      ready = browserWindow.__crystalicaClerkReady ?? Promise.resolve();
    } catch (error) {
      console.error('[Crystalica] Clerk nu a putut fi creat.', error);
    }
  }
}

export const clerk = instance;
export const clerkReady = ready;

export function readCollections(user: unknown): CollectionsMap {
  const metadata = (user as { unsafeMetadata?: Record<string, unknown> } | null | undefined)
    ?.unsafeMetadata;
  const raw = metadata?.collections;
  const collections: CollectionsMap = {};

  // Current format: "actinolit:p,agat:w". A string is used so Clerk's metadata
  // merge always replaces the previous value, which makes deletions reliable.
  if (typeof raw === 'string') {
    for (const entry of raw.split(',')) {
      const separator = entry.lastIndexOf(':');
      if (separator <= 0) continue;

      const slug = entry.slice(0, separator);
      const state = entry.slice(separator + 1);

      if (slug && (state === 'p' || state === 'w')) {
        collections[slug] = state;
      }
    }
    return collections;
  }

  // Legacy object format, kept for forward compatibility.
  if (raw && typeof raw === 'object') {
    for (const [slug, value] of Object.entries(raw as Record<string, unknown>)) {
      if (value === 'p' || value === 'w') {
        collections[slug] = value;
      }
    }
  }

  return collections;
}

export function currentCollections(): CollectionsMap {
  return readCollections(clerk?.user);
}

export async function saveCollections(
  user: { unsafeMetadata?: Record<string, unknown>; update: (data: any) => Promise<unknown> },
  collections: CollectionsMap,
): Promise<void> {
  const unsafeMetadata = {
    ...(user.unsafeMetadata ?? {}),
    collections: Object.entries(collections)
      .map(([slug, state]) => `${slug}:${state}`)
      .join(','),
  };

  await user.update({ unsafeMetadata });
  document.dispatchEvent(
    new CustomEvent<CollectionsMap>('crystalica:collections', { detail: collections }),
  );
}
