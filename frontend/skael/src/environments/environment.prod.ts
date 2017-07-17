export const environment = {
  production: true,
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
