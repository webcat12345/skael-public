export class SignupInfo {
  public email: string;
  public username: string;
  public plaintext_password: string;

  constructor() {
    this.email = '';
    this.username = '';
    this.plaintext_password = '';
  }
}
