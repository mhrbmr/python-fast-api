from passlib.context import CryptContext

password_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

class Hash():
  def bcrypt(password: str) -> str:
    return password_context.hash(password)


  def verify(sent_pass, hashed_pass):
    return password_context.verify(sent_pass, hashed_pass)