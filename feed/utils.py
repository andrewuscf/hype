from feed.models import Interest, Category


def fb_data(data, user):
    for items in data:
        photos = []
        # get category
        category = {k: v for (k, v) in items.iteritems() if 'category' in k}
        for k, d in category.iteritems():
            category_type = d

        # get photo
        photo = {k: v for (k, v) in items.iteritems() if 'photo' in k}
        for k, d in photo.iteritems():
            for x in range(0, 5):
                try:
                    photos.append(d['data'][x]['source'])
                except IndexError:
                    pass

        # get name
        name = {k: v for (k, v) in items.iteritems() if 'name' in k}
        for k, d in name.iteritems():
            name = d

        interest_insert_update(user, name, photos, category_type, 'Facebook')


def related_count_for(user_one, user_two):
    related_interest = Interest.objects.filter(user=user_one).filter(user=user_two).count()
    related_subs = Interest.objects.filter(user=user_one).filter(user=user_two).count()
    related_music = Interest.objects.filter(user=user_one).filter(user=user_two).count()
    return related_interest + related_subs + related_music


def interest_insert_update(user, name, photos, category_type, source):
    if not Category.objects.filter(name=category_type).exists():
        Category.objects.create(name=category_type)

    name = name.title()

    # check if interest exists and add user or all interest
    if Interest.objects.filter(name=name, source=source).exists():
        interest = Interest.objects.get(name=name, source=source)
        interest.user.add(user)
    else:
        category = Category.objects.get(name=category_type)
        interest = Interest.objects.create(name=name, category=category, source=source)
        for photo in photos:
            if not interest.images.filter(url=photo).exists():
                interest.images.create(url=photo)
        interest.user.add(user)
