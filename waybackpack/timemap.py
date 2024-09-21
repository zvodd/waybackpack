import logging

from .session import Session
from .exception import WaybackpackException

logger = logging.getLogger(__name__)

TIMEMAP_URL = "https://web.archive.org/web/timemap/json"


#url=example.com&matchType=prefix&collapse=urlkey&output=json&fl=original%2Cmimetype%2Ctimestamp%2Cendtimestamp%2Cgroupcount%2Cuniqcount&filter=!statuscode%3A%5B45%5D..

def timemap(
    url, from_date=None, to_date=None, collapse=None, session=None, matchType=None
):
    
        session = session or Session()
        res = session.get(
            TIMEMAP_URL,
            params={
                "url": url,
                "from": from_date,
                "to": to_date,
                "collapse": collapse,
                "matchType": matchType,
                "filter":"!statuscode:[45]..",
                "fl": "original,timestamp,endtimestamp" #,groupcount,uniqcount",
            },
        )
        
        if res is None:
            raise WaybackpackException("Difficulty connecting to Wayback Machine CDX API")
    
        if res.status_code == 200:
            cdx = res.json()
    
        else:
            log_msg = 'CDX exception: "{0}"'
            logger.info(log_msg.format(res.content.decode("utf-8").strip()))
            return []
    
        if len(cdx) < 2:
            return []
        fields = cdx[0]
        entires = [dict(zip(fields, row)) for row in cdx[1:]]
        return entires