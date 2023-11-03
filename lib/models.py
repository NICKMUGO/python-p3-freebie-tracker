from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)
company_dev = Table(
    'comany_devs',
    Base.metadata,
    Column('company_id', ForeignKey('companies.id'), primary_key=True),
    Column('user_id', ForeignKey('devs.id'), primary_key=True),
    extend_existing=True,
)


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())
    freebies = relationship('freebie', backref='company')
    devs = relationship('Dev', secondary='company_devs', back_populates='devs')

    def give_freebie(self, dev, item_name, value):
        new_freebie = freebie(dev=dev, item_name=item_name, value=value, company=self)
        return new_freebie
    
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()

    def __repr__(self):
        return f'<Company {self.name}>'

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())
    freebies = relationship('freebie',  backref='dev')
    companies = relationship('Company', secondary='company_devs', back_populates='companies')
    def received_one(self, item_name):
        for freebie in self.freebies:
            if freebie.item_name == item_name:
                return True
        return False
    
    def give_away(self, other_dev, freebie):
        if freebie.dev == self:
            freebie.dev = other_dev
    def __repr__(self):
        return f'<Dev {self.name}>'
class freebie(Base):
    __tablename__ = 'Freebie'

    id = Column(Integer(), primary_key=True)
    item_name= Column(String())
    value=Column(Integer())
    
    company_id = Column(Integer(), ForeignKey('companies.id'))
    dev_id = Column(Integer(), ForeignKey('devs.id'))
    dev = relationship('Dev',  backref='freebies')
    company = relationship('Company', backref='freebies')
    
    def __repr__(self):
        return f'<Dev {self.name}>'
