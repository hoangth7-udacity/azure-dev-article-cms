from datetime import datetime
from FlaskWebProject import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
import string, random
from werkzeug.utils import secure_filename
from flask import flash


def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(75))
    body = db.Column(db.String(800))
    image_path = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return "<Post {}>".format(self.body)

    def save_changes(self, form, file, userId, new=False):
        self.title = form.title.data
        self.author = form.author.data
        self.body = form.body.data
        self.user_id = userId

        if file:
            filename = secure_filename(file.filename)
            file_extension = filename.rsplit(".", 1)[1]
            random_filename = id_generator()
            filename = random_filename + "." + file_extension
            try:
                blob_service_client = BlobServiceClient(
                    account_url=f"https://{app.config['BLOB_ACCOUNT']}.blob.core.windows.net",
                    credential=app.config["BLOB_STORAGE_KEY"],
                )
                blob_container_client = blob_service_client.get_container_client(
                    container=app.config["BLOB_CONTAINER"]
                )
                blob_client = blob_container_client.get_blob_client(filename)
                blob_client.upload_blob(file)
                if self.image_path:
                    blob_client = blob_container_client.get_blob_client(self.image_path)
                    blob_client.delete_blob()
            except ResourceNotFoundError as e:
                app.logger.warn(f"Blob not found: {self.image_path} - Error: {e}")
            except Exception as e:
                app.logger.error(
                    "failed when uploading image to blob storage, error: %s", str(e)
                )
                flash(Exception)
            self.image_path = filename
        if new:
            db.session.add(self)
        db.session.commit()
