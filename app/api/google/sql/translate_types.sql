with
set_data as (
  select
    unnest(['local_government_office', 'natural_feature', 'point_of_interest', 'store',
    'aquarium', 'church', 'park', 'amusement_park', 'clothing_store',
    'general_contractor', 'restaurant', 'hindu_temple', 'city_hall', 'campground',
    'cemetery', 'doctor', 'night_club', 'lodging', 'bar', 'subway_station', 'museum', 'train_station',
    'grocery_or_supermarket', 'jewelry_store', 'zoo', 'electronics_store', 'cafe', 'stadium',
    'synagogue', 'funeral_home', 'health', 'real_estate_agency', 'movie_theater', 'shopping_mall',
    'premise', 'subpremise', 'locality', 'school', 'art_gallery', 'place_of_worship', 'library', 'food']) as newtype,
    unnest(['местный орган управления', 'природная функция', 'достопримечательность', 'магазин', 'аквариум', 'церковь', 'парк', 'парк развлечений', 'магазин одежды',
	'генеральный подрядчик', 'ресторан', 'индуистский храм', 'мэрия', 'палаточный лагерь',
	'Кладбище', 'Доктор', 'Ночной клуб', 'Жилье', 'Бар', 'Станция метро', 'Музей', 'Железнодорожная станция', 'Продуктовый магазин или супермаркет',
	'магазин ювелирных изделий', 'зоопарк', 'магазин электроники', 'кафе', 'стадион', 'синагога', 'похоронный дом', 'больница',
	'агентство недвижимости', 'кинотеатр', 'торговый центр', 'помещение', 'субремизм', 'местность', 'школа',
	'картинная галерея', 'место поклонения', 'библиотека', 'еда']) as oldtype
)
update geo
set type=sd.oldtype
from set_data sd
where geo.type=sd.newtype