from sqlalchemy.orm import Session, joinedload
from app.sql_model import Article, Category
from app.schemas.schemas_articles import ArticleCreate, ArticleUpdate


# ====== Consultas ======
def get_article_by_id(db: Session, article_id: int):
    return db.query(Article).filter(Article.id == article_id).first()


def get_article_by_name(db: Session, name: str):
    return db.query(Article).filter(Article.name == name).first()


def get_article_by_category(db: Session, name: str):
    return db.query(Article, Category.name).join(Category).filter(Category.name==name).all()


def get_articles(db: Session, skip: int, limit: int):
    return (
        db.query(Article)
        .options(joinedload(Article.category))  # carga la categoría relacionada
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_articles_filter(db: Session, skip: int, limit: int, name=None, category=None, available=None):
    query = db.query(Article).options(joinedload(Article.category))   

    if name:
        query = query.filter(Article.name.ilike(f"%{name}%"))        

    if category is not None:
        query = query.filter(Article.category_id == category)        

    if available is not None:
        query = query.filter(Article.available == available)        

    articles = query.offset(skip).limit(limit).all()
    
    return articles


def get_articles_count_filter(db: Session, name=None, category=None, available=None):
    query = db.query(Article)

    if name:
        query = query.filter(Article.name.ilike(f"%{name}%"))

    if category is not None:
        query = query.filter(Article.category_id == category)

    if available is not None:
        query = query.filter(Article.available == available)

    return query.count()


def get_all_articles(db: Session):
    return db.query(Article).all() 


def get_all_articles_by_name(db: Session, name=None):
    query = db.query(Article)

    if name:
        query = query.filter(Article.name.ilike(f"%{name}%"))    

    return query.all()


# ====== Crear article ======
def create_article(db: Session, data: ArticleCreate):    

    db_article = Article(
        name = data.name,
        description = data.description,
        category_id = data.categorie_id,
        stock = data.stock,
        price = data.price,
        image_name = data.imagen,
        user_id = data.admin_id
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


# ====== Actualizar article ======
def update_article(db: Session, id: int, data: ArticleUpdate):

    db_article = db.query(Article).filter(Article.id == id).first()

    if not db_article:
        return None

    update_data = data.model_dump(exclude_unset=True)

    # Solo actualizar si el campo está presente en la request
    for key, value in update_data.items():        
        setattr(db_article, key, value)
    
    db.commit()
    db.refresh(db_article)

    return db_article