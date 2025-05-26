class User_profile:
    def __init__(self, user_id, headline, bio, location, phone, birthdate, gender, website, verified=None):
        self.user_id = user_id
        self.headline = headline
        self.bio = bio
        self.location = location
        self.phone = phone
        self.birthdate = birthdate
        self.gender = gender
        self.website = website
        self.verified = verified
