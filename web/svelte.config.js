import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: undefined,
			precompress: false,
			strict: true
		}),
		// Project-site base path on GitHub Pages. Set BASE_PATH=/precio-tortillas-mexico in CI.
		paths: {
			base: process.env.BASE_PATH || ''
		},
		prerender: {
			// The dbt docs are copied into the Pages output by CI, not by this build,
			// so ignore the footer link to them during prerender crawling.
			handleHttpError: ({ path, message }) => {
				if (path.includes('dbt-docs')) return;
				throw new Error(message);
			}
		}
	}
};

export default config;
