from sqlalchemy import Column, Integer, Text, Date, BigInteger, Boolean, Float, Numeric
from sqlalchemy.dialects.postgresql import  insert
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBUpdater:
    def __init__(self, data=None, url=None):
        self.data = data
        self.url = url
        self.engine = None

    def update_db(self, data=None):
        if data is None:
            data = self.data
        self.engine = create_engine(self.url, client_encoding="utf8")

        Session = sessionmaker(bind=self.engine)
        session = Session()
        conn = self.engine.connect()
        meta = sqlalchemy.MetaData(conn)

        main_table = sqlalchemy.Table(
            'trump_twitter_data', meta,
            Column('id', Numeric(25, 0), primary_key=True),
            Column('id_str', Text),
            Column('created_at', Date),
            Column('text', Text),
            Column('retweet_count', Numeric(25, 0)),
            Column('source', Text),
            Column('favorite_count', Numeric(25, 0)),
            Column('in_reply_to_screen_name', Text),
            Column('in_reply_to_status_id', Numeric(25, 0)),
            Column('in_reply_to_status_id_str', Text),
            Column('lang', Text),
            Column('quoted_status_id', Numeric(25, 0)),
            Column('quoted_status_id_str', Text),
            Column('truncated', Boolean),
            Column('is_retweeted', Boolean),
            Column('is_quote_status', Boolean),
            Column('positive_ratings', Float),
            Column('negative_ratings', Float),
            Column('neutral_ratings', Float),
            Column('compound_score', Float)
        )

        meta.create_all()

        for i, row in enumerate(data):
            print('Upserting {}/{}'.format(i, len(data))) if i % 200 == 0 else None
            insert_stmt = insert(main_table).values(row, id=row['id'])
            do_update_stmt = insert_stmt.on_conflict_do_update(index_elements=[main_table.c.id],
                                                               set_=row)
            session.execute(do_update_stmt)

        session.commit()
