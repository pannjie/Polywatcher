import { error } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';
const API_URL = env.API_URL;

export async function load({ params, fetch }) {
  const res = await fetch(`${API_URL}/api/user/${params.address}`);
  if (!res.ok) throw error(404, 'Could not load profile.');
  return await res.json();
}
