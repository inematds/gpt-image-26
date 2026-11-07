"""Testes do gerar.py sem chamar a API: python3 -m unittest discover tests"""
import email, io, json, sys, tempfile, unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gerar


def seco(*args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = gerar.main(list(args) + ["--seco"])
    return rc, out.getvalue(), err.getvalue()


class T(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.foto = Path(self.d, "foto.jpg"); self.foto.write_bytes(b"\xff\xd8x")
        self.circ = Path(self.d, "c.png"); self.circ.write_bytes(b"\x89PNGx")

    def corpo(self, rc, out):
        self.assertEqual(rc, 0); return json.loads(out.split("\n", 1)[1])

    def test_geracao_padrao(self):
        p = self.corpo(*seco("oi")[:2])
        self.assertEqual(p["model"], "gpt-image-2.6-flare"); self.assertNotIn("complexity", p)

    def test_svg_n1(self):
        p = self.corpo(*seco("logo", "--formato", "svg", "--n", "3", "--fundo", "transparente")[:2])
        self.assertEqual((p["n"], p["background"]), (1, "transparent"))

    def test_gif(self):
        p = self.corpo(*seco("gato", "--formato", "gif", "--quadros", "16", "--ms", "20")[:2])
        self.assertEqual((p["frame_count"], p["frame_duration_ms"]), (16, 20))

    def test_limites(self):
        for args in (["x", "--formato", "gif", "--quadros", "17"], ["x", "--formato", "gif", "--ms", "10"],
                     ["x", "--tamanho", "1000x1024"], ["x", "--tamanho", "1024x3200"],
                     ["x", "--markup", str(self.circ)], ["x", "--formato", "svg", "--editar", str(self.foto)],
                     ["x", "--editar", str(self.foto), "--markup", str(self.foto)]):
            self.assertEqual(seco(*args)[0], 2, args)

    def test_multipart_jpg(self):
        corpo, tipo = gerar.multipart({"model": "m", "image": str(self.foto), "markup": str(self.circ)})
        m = email.message_from_bytes(b"Content-Type: " + tipo.encode() + b"\r\n\r\n" + corpo)
        tipos = {p.get_param("name", header="content-disposition"): p.get_content_type() for p in m.get_payload()}
        self.assertEqual(tipos["image"], "image/jpeg"); self.assertEqual(tipos["markup"], "image/png")


if __name__ == "__main__":
    unittest.main()
