from Packet import Packet


data = [i.to_bytes(1,'big') for i in range(128)]
pack = Packet(1)
pack.set_crc_mode(True)
pack.set_content(data)
print(pack.calculate_crc().value)
# for msg in pack.content:
#     print(msg.value)


pack2 = Packet(1)


pack2.from_bytes(
    pack.get_bytes()
)
print(pack2.calculate_crc().value)
print(pack2.is_valid())
#
# for msg in pack2.content:
#     print(msg.ch)





