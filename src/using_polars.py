import polars as pl

# Created by Koen Vossen, 
# Github: https://github.com/koenvo
# Twitter/x Handle: https://twitter.com/mr_le_fox
# https://x.com/mr_le_fox/status/1741893400947839362?s=20
def create_polars_df():
    pl.Config.set_streaming_chunk_size(4000000)
    return (
        
        pl.scan_csv("data/measurements.txt", separator=";", has_header=False, new_columns=["station", "measure"], schema={"station": pl.String, "measure": pl.Float64})
        .group_by(by="station")
        .agg(
            max = pl.col("measure").max(),
            min = pl.col("measure").min(),
            mean = pl.col("measure").mean()
        )
        .sort("station")
        .collect(streaming=True)
    )

if __name__ == "__main__":
    import time

    start_time = time.time()
    df = create_polars_df()
    took = time.time() - start_time
    print(df)
    print(f"Polars Took: {took:.2f} sec")