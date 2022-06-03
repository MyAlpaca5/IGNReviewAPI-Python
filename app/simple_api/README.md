# API Service
This service provides API service utilizing local database.

## Assumptions
- network traffic is handled by some external services. Network is stable and reliable, and traffic send to this API service could be reasonable large but will not overwhelm the service (load balance is handled by other service). 
- user has already been authenticated and authorized by some external services. All user request is authorized but still could be invalid.
- all user request is GET request. User can only query data from database but cannot update or insert data in database.
    - this assumption is important, it has great impact on how I design the database indexing, cache structure, and api endpoints

## Cache Mechanism
Because this project only allows user to request data but not update or insert new data, so a cache could dramatically improve the query performance. Due to the size and simplicity of this project, using a full-blown third-party cache library could be overkill for this project. Therefore, I implement a simple LFU (least frequently used) cache to store searched query and returned database objects.

## API Endpoints
This service exposes three endpoints, `reviews`, `mediatype`, and `publisher`

*Note: API information is also available in `/docs` path with Swagger.*

### Review Endpoint
Get review record(s).

`GET /reivews/:id`

Path Parameter(s)
| Name           | Type     | Required |
| -------------- | -------- | -------- |
| `id`           | `Number` | False    |

Query Parameter(s)
| Name           | Type     | Description                     | Required |
| -------------- | -------- | ------------------------------- | -------- |
| `media_type_id`| `Number` | The unique id for media type    | False    |
| `publisher_id` | `Number` | The unique id for publisehr     | False    |
| `posted_year`  | `Number` | The year that review was posted | False    |
| `score`        | `Number` | The minimum score for review    | False    |

Example Request with Path Parameter(s)

`GET /reviews/4`

Example Response
```
{
  "name": "A Hidden Life",
  "short_name": "A Hidden Life",
  "long_description": "A didden life of an unsung hero",
  "created_at": "2019-11-12T16:46:40.821000",
  "updated_at": "2019-11-12T16:50:43.556000",
  "review_url": "https://www.ign.com/articles/2019/12/11/a-hidden-life-review",
  "review_score": 8.5,
  "slug": "a-hidden-life",
  "media_type": {
    "type_name": "Movie"
  },
  "genres": [
    {
      "genre_name": "Drama"
    }
  ],
  "creators": [],
  "publishers": [
    {
      "publisher_name": "Fox Searchlight Pictures"
    }
  ],
  "franchises": [],
  "regions": []
}
```

Example Request with Query Parameter(s)

`GET /reviews/?media_type_id=3&publisher_id=6&posted_year=2019`

*Note: return list will be sorted by score then review name in descending order.*

Example Response
```
[
  {
    "name": "Scrawl",
    "short_name": "Scrawl",
    "long_description": "Magic stuff.",
    "short_description": "Magic stuff.",
    "created_at": "2019-06-27T12:46:17.049000",
    "updated_at": "2019-06-27T16:22:36.081000",
    "review_url": "https://www.ign.com/articles/2019/06/27/scrawl-review-daisy-ridley-movie",
    "review_score": 2,
    "slug": "scrawl",
    "media_type": {
      "type_name": "Movie"
    },
    "genres": [
      {
        "genre_name": "Horror"
      }
    ],
    "creators": [],
    "publishers": [
      {
        "publisher_name": "Wild Eye Releasing"
      }
    ],
    "franchises": [],
    "regions": []
  }
]
```

### Media Type Endpoint
Get media type overview.

`GET /mediatype/`

Example Response
```
{
  "size": 4,
  "items": [
    [
      1,
      "Comic"
    ],
    [
      2,
      "Show"
    ]
  ]
}
```

Get one media type object.

`GET /mediatype/:id`

Path Parameter(s)
| Name           | Type     | Required |
| -------------- | -------- | -------- |
| `id`           | `Number` | False    |

Example Request with Path Parameter(s)

`GET /mediatype/3`

Example Response
```
{
  "type_name": "Movie",
  "reviews": [
    {
      "name": "1917",
      "short_name": "1917",
      "long_description": "First World War Event.",
      "short_description": "First World War Event.",
      "created_at": "2018-12-13T17:08:33.408000",
      "updated_at": "2020-01-09T12:55:52.386000",
      "review_url": "https://www.ign.com/articles/2020/01/09/1917-review",
      "review_score": 9.5,
      "slug": "1917",
      "media_type": {
        "type_name": "Movie"
      },
      "genres": [
        {
          "genre_name": "Drama"
        }
      ],
      "creators": [
        {
          "creator_name": "Amblin Entertainment"
        }
      ],
      "publishers": [
        {
          "publisher_name": "Universal Pictures"
        }
      ],
      "franchises": [],
      "regions": []
    },
    ...
  ]
}
```

### Publisher Endpoint
Get publisher overview.

`GET /publisher/`

Example Response
```
{
  "size": 136,
  "items": [
    [
      1,
      "A24"
    ],
    ...
    [
      136,
      "Cygames"
    ]
  ]
}
```

Get one publisher object.

`GET /publisher/:id`

Path Parameter(s)
| Name           | Type     | Required |
| -------------- | -------- | -------- |
| `id`           | `Number` | False    |

Example Request with Path Parameter(s)

`GET /publisher/5`

Example Response
```
{
  "publisher_name": "BigBen Interactive",
  "reviews": [
    {
      "name": "AO Tennis 2",
      "short_name": "AO Tennis 2",
      "long_description": "AO Tennis 2.",
      "short_description": "AO Tennis 2.",
      "created_at": "2019-11-07T15:07:03.666000",
      "updated_at": "2020-02-14T12:22:29.474000",
      "review_url": "https://www.ign.com/articles/2020/01/08/ao-tennis-2-review",
      "review_score": 7,
      "slug": "ao-tennis-2",
      "media_type": {
        "type_name": "Game"
      },
      "genres": [
        {
          "genre_name": "Sports"
        }
      ],
      "creators": [
        {
          "creator_name": "Big Ant Studios"
        }
      ],
      "publishers": [
        {
          "publisher_name": "BigBen Interactive"
        }
      ],
      "franchises": [],
      "regions": [
        {
          "region_name": "US"
        },
        {
          "region_name": "UK"
        },
        {
          "region_name": "JP"
        },
        {
          "region_name": "AU"
        }
      ]
    },
    ...
  ]
}
```
