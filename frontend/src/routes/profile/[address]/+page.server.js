import { error } from '@sveltejs/kit';

export async function load({ params, fetch }) {
  const res = await fetch(`${process.env.API_URL}/api/user/${params.address}`);
  if (!res.ok) throw error(404, 'Could not load profile.');
  return await res.json();
}
