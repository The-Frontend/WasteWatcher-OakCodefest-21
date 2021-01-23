from enum import Enum
from typing import Optional, List, Any, Dict, TypeVar, Callable, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


class Caution(Enum):
    FODMAP = "FODMAP"
    Sulfites = "Sulfites"


class SchemaOrgTag(Enum):
    carbohydrateContent = "carbohydrateContent"
    cholesterolContent = "cholesterolContent"
    fatContent = "fatContent"
    fiberContent = "fiberContent"
    proteinContent = "proteinContent"
    saturatedFatContent = "saturatedFatContent"
    sodiumContent = "sodiumContent"
    sugarContent = "sugarContent"
    transFatContent = "transFatContent"


class Unit(Enum):
    empty = "%"
    g = "g"
    kcal = "kcal"
    mg = "mg"
    µg = "µg"


class Digest:
    label: str
    tag: str
    schemaOrgTag: Optional[SchemaOrgTag]
    total: float
    hasRDI: bool
    daily: float
    unit: Unit
    sub: Optional[List['Digest']]

    def __init__(self, label: str, tag: str, schemaOrgTag: Optional[SchemaOrgTag], total: float, hasRDI: bool, daily: float, unit: Unit, sub: Optional[List['Digest']]) -> None:
        self.label = label
        self.tag = tag
        self.schemaOrgTag = schemaOrgTag
        self.total = total
        self.hasRDI = hasRDI
        self.daily = daily
        self.unit = unit
        self.sub = sub

    @staticmethod
    def from_dict(obj: Any) -> 'Digest':
        assert isinstance(obj, dict)
        label = from_str(obj.get("label"))
        tag = from_str(obj.get("tag"))
        schemaOrgTag = from_union([from_none, SchemaOrgTag], obj.get("schemaOrgTag"))
        total = from_float(obj.get("total"))
        hasRDI = from_bool(obj.get("hasRDI"))
        daily = from_float(obj.get("daily"))
        unit = Unit(obj.get("unit"))
        sub = from_union([lambda x: from_list(Digest.from_dict, x), from_none], obj.get("sub"))
        return Digest(label, tag, schemaOrgTag, total, hasRDI, daily, unit, sub)

    def to_dict(self) -> dict:
        result: dict = {}
        result["label"] = from_str(self.label)
        result["tag"] = from_str(self.tag)
        result["schemaOrgTag"] = from_union([from_none, lambda x: to_enum(SchemaOrgTag, x)], self.schemaOrgTag)
        result["total"] = to_float(self.total)
        result["hasRDI"] = from_bool(self.hasRDI)
        result["daily"] = to_float(self.daily)
        result["unit"] = to_enum(Unit, self.unit)
        result["sub"] = from_union([lambda x: from_list(lambda x: to_class(Digest, x), x), from_none], self.sub)
        return result


class HealthLabel(Enum):
    AlcoholFree = "Alcohol-Free"
    ImmunoSupportive = "Immuno-Supportive"
    PeanutFree = "Peanut-Free"
    SugarConscious = "Sugar-Conscious"
    TreeNutFree = "Tree-Nut-Free"


class Ingredient:
    text: str
    weight: float
    image: Optional[str]

    def __init__(self, text: str, weight: float, image: Optional[str]) -> None:
        self.text = text
        self.weight = weight
        self.image = image

    @staticmethod
    def from_dict(obj: Any) -> 'Ingredient':
        assert isinstance(obj, dict)
        text = from_str(obj.get("text"))
        weight = from_float(obj.get("weight"))
        image = from_union([from_none, from_str], obj.get("image"))
        return Ingredient(text, weight, image)

    def to_dict(self) -> dict:
        result: dict = {}
        result["text"] = from_str(self.text)
        result["weight"] = to_float(self.weight)
        result["image"] = from_union([from_none, from_str], self.image)
        return result


class Total:
    label: str
    quantity: float
    unit: Unit

    def __init__(self, label: str, quantity: float, unit: Unit) -> None:
        self.label = label
        self.quantity = quantity
        self.unit = unit

    @staticmethod
    def from_dict(obj: Any) -> 'Total':
        assert isinstance(obj, dict)
        label = from_str(obj.get("label"))
        quantity = from_float(obj.get("quantity"))
        unit = Unit(obj.get("unit"))
        return Total(label, quantity, unit)

    def to_dict(self) -> dict:
        result: dict = {}
        result["label"] = from_str(self.label)
        result["quantity"] = to_float(self.quantity)
        result["unit"] = to_enum(Unit, self.unit)
        return result


class Recipe:
    uri: str
    label: str
    image: str
    source: str
    url: str
    shareAs: str
    recipeyield: int
    dietLabels: List[str]
    healthLabels: List[HealthLabel]
    cautions: List[Caution]
    ingredientLines: List[str]
    ingredients: List[Ingredient]
    calories: float
    totalWeight: float
    totalTime: int
    totalNutrients: Dict[str, Total]
    totalDaily: Dict[str, Total]
    digest: List[Digest]

    def __init__(self, uri: str, label: str, image: str, source: str, url: str, shareAs: str, recipeyield: int, dietLabels: List[str], healthLabels: List[HealthLabel], cautions: List[Caution], ingredientLines: List[str], ingredients: List[Ingredient], calories: float, totalWeight: float, totalTime: int, totalNutrients: Dict[str, Total], totalDaily: Dict[str, Total], digest: List[Digest]) -> None:
        self.uri = uri
        self.label = label
        self.image = image
        self.source = source
        self.url = url
        self.shareAs = shareAs
        self.recipeyield = recipeyield
        self.dietLabels = dietLabels
        self.healthLabels = healthLabels
        self.cautions = cautions
        self.ingredientLines = ingredientLines
        self.ingredients = ingredients
        self.calories = calories
        self.totalWeight = totalWeight
        self.totalTime = totalTime
        self.totalNutrients = totalNutrients
        self.totalDaily = totalDaily
        self.digest = digest

    @staticmethod
    def from_dict(obj: Any) -> 'Recipe':
        assert isinstance(obj, dict)
        uri = from_str(obj.get("uri"))
        label = from_str(obj.get("label"))
        image = from_str(obj.get("image"))
        source = from_str(obj.get("source"))
        url = from_str(obj.get("url"))
        shareAs = from_str(obj.get("shareAs"))
        recipeyield = from_int(obj.get("yield"))
        dietLabels = from_list(from_str, obj.get("dietLabels"))
        healthLabels = from_list(HealthLabel, obj.get("healthLabels"))
        cautions = from_list(Caution, obj.get("cautions"))
        ingredientLines = from_list(from_str, obj.get("ingredientLines"))
        ingredients = from_list(Ingredient.from_dict, obj.get("ingredients"))
        calories = from_float(obj.get("calories"))
        totalWeight = from_float(obj.get("totalWeight"))
        totalTime = from_int(obj.get("totalTime"))
        totalNutrients = from_dict(Total.from_dict, obj.get("totalNutrients"))
        totalDaily = from_dict(Total.from_dict, obj.get("totalDaily"))
        digest = from_list(Digest.from_dict, obj.get("digest"))
        return Recipe(uri, label, image, source, url, shareAs, recipeyield, dietLabels, healthLabels, cautions, ingredientLines, ingredients, calories, totalWeight, totalTime, totalNutrients, totalDaily, digest)

    def to_dict(self) -> dict:
        result: dict = {}
        result["uri"] = from_str(self.uri)
        result["label"] = from_str(self.label)
        result["image"] = from_str(self.image)
        result["source"] = from_str(self.source)
        result["url"] = from_str(self.url)
        result["shareAs"] = from_str(self.shareAs)
        result["yield"] = from_int(self.recipeyield)
        result["dietLabels"] = from_list(from_str, self.dietLabels)
        result["healthLabels"] = from_list(lambda x: to_enum(HealthLabel, x), self.healthLabels)
        result["cautions"] = from_list(lambda x: to_enum(Caution, x), self.cautions)
        result["ingredientLines"] = from_list(from_str, self.ingredientLines)
        result["ingredients"] = from_list(lambda x: to_class(Ingredient, x), self.ingredients)
        result["calories"] = to_float(self.calories)
        result["totalWeight"] = to_float(self.totalWeight)
        result["totalTime"] = from_int(self.totalTime)
        result["totalNutrients"] = from_dict(lambda x: to_class(Total, x), self.totalNutrients)
        result["totalDaily"] = from_dict(lambda x: to_class(Total, x), self.totalDaily)
        result["digest"] = from_list(lambda x: to_class(Digest, x), self.digest)
        return result


class Hit:
    recipe: Recipe
    bookmarked: bool
    bought: bool

    def __init__(self, recipe: Recipe, bookmarked: bool, bought: bool) -> None:
        self.recipe = recipe
        self.bookmarked = bookmarked
        self.bought = bought

    @staticmethod
    def from_dict(obj: Any) -> 'Hit':
        assert isinstance(obj, dict)
        recipe = Recipe.from_dict(obj.get("recipe"))
        bookmarked = from_bool(obj.get("bookmarked"))
        bought = from_bool(obj.get("bought"))
        return Hit(recipe, bookmarked, bought)

    def to_dict(self) -> dict:
        result: dict = {}
        result["recipe"] = to_class(Recipe, self.recipe)
        result["bookmarked"] = from_bool(self.bookmarked)
        result["bought"] = from_bool(self.bought)
        return result


class EdamamAPIResponse:
    q: str
    EdamamAPIResponsefrom: int
    to: int
    more: bool
    count: int
    hits: List[Hit]

    def __init__(self, q: str, EdamamAPIResponsefrom: int, to: int, more: bool, count: int, hits: List[Hit]) -> None:
        self.q = q
        self.EdamamAPIResponsefrom = EdamamAPIResponsefrom
        self.to = to
        self.more = more
        self.count = count
        self.hits = hits

    @staticmethod
    def from_dict(obj: Any) -> 'EdamamAPIResponse':
        assert isinstance(obj, dict)
        q = from_str(obj.get("q"))
        EdamamAPIResponsefrom = from_int(obj.get("from"))
        to = from_int(obj.get("to"))
        more = from_bool(obj.get("more"))
        count = from_int(obj.get("count"))
        hits = from_list(Hit.from_dict, obj.get("hits"))
        return EdamamAPIResponse(q, EdamamAPIResponsefrom, to, more, count, hits)

    def to_dict(self) -> dict:
        result: dict = {}
        result["q"] = from_str(self.q)
        result["from"] = from_int(self.EdamamAPIResponsefrom)
        result["to"] = from_int(self.to)
        result["more"] = from_bool(self.more)
        result["count"] = from_int(self.count)
        result["hits"] = from_list(lambda x: to_class(Hit, x), self.hits)
        return result


def EdamamAPIResponsefromdict(s: Any) -> EdamamAPIResponse:
    return EdamamAPIResponse.from_dict(s)


def EdamamAPIResponsetodict(x: EdamamAPIResponse) -> Any:
    return to_class(EdamamAPIResponse, x)