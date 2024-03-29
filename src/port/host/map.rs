use std::collections::HashMap;
use std::vec::Vec;

pub type MapValue = (u16, u16, Option<Vec<u16>>);
pub type Map = HashMap<String, MapValue>;

pub fn tcp_map_create() -> Map {
    HashMap::from([
        ("full".to_string(), (0, 65535, None)),
        ("fast".to_string(), (0, 1023, None)),
        ("test".to_string(), (0, 0, Some(vec![8080]))),
    ])
}

pub fn udp_map_create() -> Map {
    HashMap::from([
        ("full".to_string(), (0, 65535, None)),
        ("fast".to_string(), (0, 1023, None)),
        ("test".to_string(), (0, 0, Some(vec![0]))),
    ])
}
