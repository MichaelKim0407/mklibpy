# App Manager

Dynamically enable/disable apps.

## Concept

This app contains a middleware that checks `app_name` for a request url.

If the `app_name` is set to inactive, then the response will be 404.

## Usage

In `settings.py`:

* Add to `INSTALLED_APPS`

    ```
    INSTALLED_APPS = [
        ...
        'mklibpy.django.app_manager',
    ]
    ```

* Add interceptor middleware

    ```
    MIDDLEWARE = [
        ...
        'mklibpy.django.app_manager.intercept.AppNameInterceptor',
    ]
    ```

* Specify whether unregistered apps will be intercepted

    ```
    APP_MANAGER_INTERCEPT_UNREGISTERED = True
    ```

    Default is `False`.

* Specify whether app-less urls will be intercepted

    ```
    APP_MANAGER_INTERCEPT_NOAPP = True
    ```

    Default is `False`.

    This option is in the settings, but it's probably not a good idea to set it to `True`...

Run migrations:

```
python manage.py migrate
```

## Manage

Manage apps using django site admin.

`name` should be the `app_name` specified in your app's url module.

`order` is a currently a placeholder.

**Don't** delete or deactivate the `admin` app! Otherwise you will lose access to your site administration.
