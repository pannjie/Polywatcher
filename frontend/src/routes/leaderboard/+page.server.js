import { error } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
const API_URL = env.API_URL;

export async function load({ fetch }) {
  const res = await fetch(`${API_URL}/api/leaderboard-results`);
  if (!res.ok) throw error(500, 'Could not load leaderboard.');
  return { wallets: await res.json() };
}
