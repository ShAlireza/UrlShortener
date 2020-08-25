from ..models import ShortenedURL

__all__ = ('ShortenedURLService',)


class ShortenedURLService:

    @staticmethod
    def id_to_short_url(obj: ShortenedURL):
        # Encode obj id to a number in base 62(alphanumeric character sequence)
        dictionary = ("abcdefghijklmnopqrstuvwxyz"
                      "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                      "0123456789")
        base = len(dictionary)

        obj_id = obj.id
        key = ''
        while obj_id > 0:
            key += dictionary[obj_id % base]
            obj_id //= base

        return key[len(key)::-1]

    @staticmethod
    def short_url_to_id(key, base=62):
        obj_id = 0
        for char in key:
            if 'a' <= char <= 'z':
                obj_id = obj_id * base + ord(char) - ord('a')
            elif 'A' <= char <= 'Z':
                obj_id = obj_id * base + ord(char) - ord('A') + 26
            else:
                obj_id = obj_id * base + ord(char) - ord('0') + 52
        return obj_id
