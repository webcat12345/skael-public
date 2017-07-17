// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.

export const environment = {
  production: false,
  localStorage: {
    prefix: 'SKAEL', // prefix
    token: 'AUTH_TOKEN', // token storage
    user_info: 'ME' // authenticated user info
  },
  cookie: {
    storage: 'SKAEL', // cookie storage
    value: 'DK383932NVM', // cookie key
    life: 5 // life cycle of cookie days
  },
  baseAPIUrl: 'http://107.170.200.188/'
};
