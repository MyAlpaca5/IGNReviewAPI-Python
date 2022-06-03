import pytest

from app.simple_api.cache import Node, DLL, LFUCache


@pytest.mark.parametrize(
    "nodes", [
        [(0, "only")],
        [(1, "first"), (2, "second"), (3, "third")],
        [(1, "first"), (3, "three"), (5, "five"), (999, "last")],
    ]
)
def test_ddl(nodes):
    ddl = DLL()

    for key, val in nodes:
        node = Node(key=key, value=val)
        ddl.append(node)

    assert ddl.head.key == nodes[0][0]
    assert ddl.head.value == nodes[0][1]
    assert ddl.tail.key == nodes[-1][0]
    assert ddl.tail.value == nodes[-1][1]

    # delete head
    ddl.delete_head()

    if len(nodes) == 1:
        # if we only insert one node before,
        # then after deletion, ddl should be empty
        assert ddl.head is None
        assert ddl.tail is None
    else:
        assert ddl.head.key == nodes[1][0]
        assert ddl.head.value == nodes[1][1]
        assert ddl.tail.key == nodes[-1][0]
        assert ddl.tail.value == nodes[-1][1]


# operation --> a list of (action, key)
# action --> 0, get; 1, put;
operation_1 = [(1, 1), (1, 2), (0, 1), (1, 3), (0, 2), (0, 3)]
operation_2 = [(1, 1), (1, 2), (0, 2), (1, 3), (0, 1), (0, 3), (1, 4)]
operation_3 = [(1, 1), (1, 2), (0, 2), (1, 3), (0, 1), (0, 3), (1, 4), (0, 1), (1, 5), (0, 5), (1, 2)]

# result --> least_freq, a list of (key, freq)
# # Note: when freq == None, key is not presented in node_map
result_1 = {"least_freq": 2, "results": [(1, 2), (2, 2), (3, 2)]}
result_2 = {"least_freq": 1, "results": [(4, 1), (1, 2), (3, 2)]}
result_3 = {"least_freq": 1, "results": [(2, 1), (5, 2), (1, 3)]}


@pytest.mark.parametrize(
    "operation, result", [
        (operation_1, result_1),
        (operation_2, result_2),
        (operation_3, result_3),
    ]
)
def test_lfu_cache(operation, result):
    lfu = LFUCache[int, int](3)

    for action, key in operation:
        if action == 0:
            lfu.get(key)
        else:
            lfu.put(key)

    assert result["least_freq"] == lfu.least_freq

    for key, freq in result["results"]:
        if freq == 0:
            assert key not in lfu.node_map
        else:
            assert lfu.node_map[key].freq == freq
