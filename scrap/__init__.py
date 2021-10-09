if __package__:
    from . import gov_price
else:
    import gov_price

def main(cfg):
    gov_price.main(**cfg['gov_price'])