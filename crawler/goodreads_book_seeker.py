import crawler.knowledgeseeker as ks

# Setup goodreads API
KEY = '83miVYXm5ohZqeANTj0hLw'
SECRET = 'x5gbome6DgF2fZfiVHuQrfxndTzFQ4cMBM9EdufS1A'

seeker = ks.KnowledgeSeeker((KEY, SECRET), api_type="goodreads")

seeker.gather_knowledge("userlist_2")


# amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)
