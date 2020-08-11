from scraper.models import Session, Job


def get_scraped_ids(site):
    session = Session()
    ids = [j.job_id for j in session.query(Job.job_id).filter_by(site=site).order_by(Job.job_id)]
    # print(ids)
    # session.close()
    # print("Got existing IDS in DB, to avoid saving duplicates... [" + str(len(ids)) + "]")
    return ids