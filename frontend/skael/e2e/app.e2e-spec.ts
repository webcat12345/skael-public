import { SkaelPage } from './app.po';

describe('skael App', () => {
  let page: SkaelPage;

  beforeEach(() => {
    page = new SkaelPage();
  });

  it('should display welcome message', done => {
    page.navigateTo();
    page.getParagraphText()
      .then(msg => expect(msg).toEqual('Welcome to app!!'))
      .then(done, done.fail);
  });
});
